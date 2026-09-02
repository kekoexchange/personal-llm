import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import MessageArea from '../src/components/MessageArea';

const SEPARATOR = '\n====================\n';

function transcript(container) {
  return container.querySelector('code').textContent;
}

describe('MessageArea', () => {
  it('shows each history entry followed by a separator, then the current message', () => {
    const { container } = render(
      <MessageArea messageHistory={['user: hi', 'assistant: hello']} currentMessage="assistant: typ" />
    );

    expect(transcript(container)).toBe(
      'user: hi' + SEPARATOR + 'assistant: hello' + SEPARATOR + 'assistant: typ'
    );
  });

  it('shows only the current message when there is no history', () => {
    const { container } = render(<MessageArea messageHistory={[]} currentMessage="assistant: " />);

    expect(transcript(container)).toBe('assistant: ');
  });

  it('is empty for a brand new chat', () => {
    const { container } = render(<MessageArea messageHistory={[]} currentMessage="" />);

    expect(transcript(container)).toBe('');
  });
});
