import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ChatList from '../src/components/ChatList';

const chats = [
  { id: 1, name: 'Shopping list' },
  { id: 2, name: 'Python help' },
];

describe('ChatList', () => {
  it('renders one entry per chat', () => {
    render(<ChatList allChats={chats} currentChatID={0} onChatSelect={() => {}} />);

    const items = screen.getAllByRole('listitem');
    expect(items.map((li) => li.textContent)).toEqual(['Shopping list', 'Python help']);
  });

  it('renders nothing in the list when there are no chats', () => {
    render(<ChatList allChats={[]} currentChatID={0} onChatSelect={() => {}} />);

    expect(screen.queryAllByRole('listitem')).toHaveLength(0);
  });

  it('calls onChatSelect with the id of the clicked chat', () => {
    const onChatSelect = vi.fn();
    render(<ChatList allChats={chats} currentChatID={0} onChatSelect={onChatSelect} />);

    fireEvent.click(screen.getByText('Python help'));

    expect(onChatSelect).toHaveBeenCalledWith(2);
  });

  it('marks the current chat as selected', () => {
    render(<ChatList allChats={chats} currentChatID={2} onChatSelect={() => {}} />);

    expect(screen.getByText('Python help')).toHaveClass('selected');
    expect(screen.getByText('Shopping list')).not.toHaveClass('selected');
  });
});
