// Runs before every frontend test file (see vitest.config.mjs).
//
// WARNING: when the app starts, python-eel scans every .js file under
// frontend/ (this folder included, comments included) for the text
// "eel.expose" followed by "(" and registers whatever name comes after it as
// a browser function. Never write that text in this folder, not even in a
// comment, or the app will register a phantom function or crash on start-up.
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';

// In the real app Python-Eel injects a global `eel` object into the page
// (frontend/index.html loads eel.js). Calling a backend function looks like
//
//     eel.py_get_chats()(callback)     // first call = arguments, second = callback
//
// and the backend calls browser functions that were registered with
// eel's expose function. This fake copies that shape so
// frontend/src/api/functions.js runs unchanged. In tests:
//
//     eel.py_create_chat.returns({ id: 7, name: 'hello' })   // choose the reply
//     expect(eel.py_create_chat).toHaveBeenCalledWith('hello')
//     eel.exposed.jsUpdateCurrentMessage('chunk')            // backend -> browser

const DEFAULT_RESULTS = {
  py_send_message: undefined,
  py_delete_chat: undefined,
  py_get_chats: [],
  py_get_messages_by_chat: [],
  py_create_chat: (name) => ({ id: 1, name, created_at: '2026-01-01T00:00:00' }),
};

function fakeEelFunction() {
  const fn = vi.fn((...args) => (callback = () => {}) => {
    const result = fn.result;
    callback(typeof result === 'function' ? result(...args) : result);
  });
  fn.returns = (value) => {
    fn.result = value;
    return fn;
  };
  return fn;
}

const eel = {
  exposed: {},
  expose(fn, name = fn.name) {
    eel.exposed[name] = fn;
  },
};
for (const name of Object.keys(DEFAULT_RESULTS)) {
  eel[name] = fakeEelFunction();
}
globalThis.eel = eel;

beforeEach(() => {
  // forget calls and replies from the previous test
  for (const [name, value] of Object.entries(DEFAULT_RESULTS)) {
    eel[name].mockClear();
    eel[name].returns(value);
  }
});

afterEach(cleanup); // unmount whatever the previous test rendered
