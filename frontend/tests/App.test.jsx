import { render, screen, fireEvent, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../src/App';

// `eel` is the fake backend from ./setup.js
const eel = globalThis.eel;

function transcript() {
  return document.querySelector('code').textContent;
}

function typeAndSend(text) {
  fireEvent.change(screen.getByLabelText('Message'), { target: { value: text } });
  fireEvent.click(screen.getByRole('button', { name: 'Send' }));
}

describe('App', () => {
  it('loads the chat list from the backend on start-up', () => {
    eel.py_get_chats.returns([
      { id: 3, name: 'Earlier chat' },
      { id: 4, name: 'Another chat' },
    ]);

    render(<App />);

    expect(eel.py_get_chats).toHaveBeenCalledTimes(1);
    expect(screen.getByText('Earlier chat')).toBeInTheDocument();
    expect(screen.getByText('Another chat')).toBeInTheDocument();
  });

  it('first message: creates a chat named after the text, then sends the message to it', () => {
    eel.py_create_chat.returns({ id: 7, name: 'A rather long first' });
    render(<App />);

    typeAndSend('A rather long first message, longer than twenty characters');

    // chat name is the first 20 characters of the message
    expect(eel.py_create_chat).toHaveBeenCalledWith('A rather long first ');
    expect(eel.py_send_message).toHaveBeenCalledWith(
      'A rather long first message, longer than twenty characters',
      7
    );
    // the new chat appears in the list
    expect(screen.getByText('A rather long first')).toBeInTheDocument();
    // the transcript shows the user's message and an empty assistant line
    expect(transcript()).toBe(
      'user: A rather long first message, longer than twenty characters' +
        '\n====================\n' +
        'assistant: '
    );
  });

  it('streamed chunks from the backend are appended to the assistant line', () => {
    render(<App />);
    typeAndSend('hi');

    // this is what the Python side calls (see js_update_current_message)
    act(() => eel.exposed.jsUpdateCurrentMessage('Hel'));
    act(() => eel.exposed.jsUpdateCurrentMessage('lo!'));

    expect(transcript()).toBe('user: hi\n====================\nassistant: Hello!');
  });

  it('a second message goes to the same chat without creating another one', () => {
    eel.py_create_chat.returns({ id: 7, name: 'hi' });
    render(<App />);
    typeAndSend('hi');
    act(() => eel.exposed.jsUpdateCurrentMessage('Hello!'));

    typeAndSend('how are you?');

    expect(eel.py_create_chat).toHaveBeenCalledTimes(1);
    expect(eel.py_send_message).toHaveBeenLastCalledWith('how are you?', 7);
    // the finished assistant reply moved into the history, above the new user line
    expect(transcript()).toBe(
      'user: hi\n====================\n' +
        'assistant: Hello!\n====================\n' +
        '\nuser: how are you?\n====================\n' +
        'assistant: '
    );
  });

  it('selecting a chat loads its messages', () => {
    eel.py_get_chats.returns([{ id: 3, name: 'Earlier chat' }]);
    eel.py_get_messages_by_chat.returns([
      { id: 10, role: 'user', content: 'what is 2+2?' },
      { id: 11, role: 'assistant', content: '4' },
    ]);
    render(<App />);

    fireEvent.click(screen.getByText('Earlier chat'));

    expect(eel.py_get_messages_by_chat).toHaveBeenCalledWith(3);
    expect(screen.getByText('Earlier chat')).toHaveClass('selected');
    expect(transcript()).toBe(
      'user: what is 2+2?\n====================\nassistant: 4\n====================\n'
    );
  });

  it('a message sent from a selected chat goes to that chat', () => {
    eel.py_get_chats.returns([{ id: 3, name: 'Earlier chat' }]);
    render(<App />);
    fireEvent.click(screen.getByText('Earlier chat'));

    typeAndSend('again');

    expect(eel.py_create_chat).not.toHaveBeenCalled();
    expect(eel.py_send_message).toHaveBeenCalledWith('again', 3);
  });

  it('Delete Chat removes the selected chat and returns to a new chat', () => {
    eel.py_get_chats.returns([
      { id: 3, name: 'Earlier chat' },
      { id: 4, name: 'Another chat' },
    ]);
    render(<App />);
    fireEvent.click(screen.getByText('Earlier chat'));

    fireEvent.click(screen.getByRole('button', { name: 'Delete Chat' }));

    expect(eel.py_delete_chat).toHaveBeenCalledWith(3);
    expect(screen.queryByText('Earlier chat')).not.toBeInTheDocument();
    expect(screen.getByText('Another chat')).toBeInTheDocument();
    expect(transcript()).toBe('');
  });
});
