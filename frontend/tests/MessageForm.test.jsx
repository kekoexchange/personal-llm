import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import MessageForm from '../src/components/MessageForm';

function renderForm() {
  const props = { onSubmitForm: vi.fn(), onDeleteChat: vi.fn(), onNewChat: vi.fn() };
  render(<MessageForm {...props} />);
  return { ...props, textarea: screen.getByLabelText('Message') };
}

describe('MessageForm', () => {
  it('shows what the user types', () => {
    const { textarea } = renderForm();

    fireEvent.change(textarea, { target: { value: 'hello there' } });

    expect(textarea).toHaveValue('hello there');
  });

  it('clicking Send submits the text as typed and clears the box', () => {
    const { textarea, onSubmitForm } = renderForm();
    fireEvent.change(textarea, { target: { value: '  hello  ' } });

    fireEvent.click(screen.getByRole('button', { name: 'Send' }));

    // the form does not trim: whatever was typed is sent
    expect(onSubmitForm).toHaveBeenCalledWith('  hello  ');
    expect(textarea).toHaveValue('');
  });

  it('pressing Enter submits', () => {
    const { textarea, onSubmitForm } = renderForm();
    fireEvent.change(textarea, { target: { value: 'hello' } });

    fireEvent.keyDown(textarea, { key: 'Enter', keyCode: 13 });

    expect(onSubmitForm).toHaveBeenCalledWith('hello');
    expect(textarea).toHaveValue('');
  });

  it('pressing Shift+Enter does not submit (it is for a new line)', () => {
    const { textarea, onSubmitForm } = renderForm();
    fireEvent.change(textarea, { target: { value: 'hello' } });

    fireEvent.keyDown(textarea, { key: 'Enter', keyCode: 13, shiftKey: true });

    expect(onSubmitForm).not.toHaveBeenCalled();
    expect(textarea).toHaveValue('hello');
  });

  it('Delete Chat and New Chat call their callbacks without submitting', () => {
    const { textarea, onDeleteChat, onNewChat, onSubmitForm } = renderForm();
    fireEvent.change(textarea, { target: { value: 'half-typed' } });

    fireEvent.click(screen.getByRole('button', { name: 'Delete Chat' }));
    fireEvent.click(screen.getByRole('button', { name: 'New Chat' }));

    expect(onDeleteChat).toHaveBeenCalledTimes(1);
    expect(onNewChat).toHaveBeenCalledTimes(1);
    expect(onSubmitForm).not.toHaveBeenCalled();
    // Today the typed text is NOT cleared by these buttons: both handlers call
    // setMessageValue() with no argument, which does not reset the box. This
    // asserts the current behaviour; if you fix MessageForm.jsx, change it to ''.
    expect(textarea).toHaveValue('half-typed');
  });
});
