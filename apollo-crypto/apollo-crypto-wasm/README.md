## Crypto module for Apollo Voting

The core algorithms are implemented in Rust which is then compiled to WebAssembly and
used from JavaScript as a normal module.

### Project structure

The Rust code is inside the `src` directory and it is compiled normally to `target`.
During compilation, a second directory - `pkg` - is updated with the current JavaScript/TypeScript
interface of the library and a standalone WASM file. Note that the compilation process
is slightly different than simply calling `cargo build`.

The contents of the `pkg` directory are a well-defined JavaScript module that can be imported
as a third-party package in other places. More on that later.


### Installation

First, prepare the Rust environment by following the steps specified [here](https://rustwasm.github.io/book/game-of-life/setup.html).

Then, enter `www` and call `npm install` to prepare all the dependencies.

### Development

When you inspect `www/package.json`, you can see that there is a dependency called `apollo-crypto`
that points to the `pkg` directory. This will enable hot-reloading of the webpage whenever
you recompile the Rust code.

The compilation process is done by calling `wasm-pack build`. It performs mostly the same as
`cargo build` but it additionally updates the `pkg` dir with newly generated interfaces and
WASM.

To run the development server, call `npm run start` while inside `www` and visit `localhost:8080`.
If you need to use a different port, you can specify it manually by calling `npm run start -- --port=PORT`.
