`protobuf-inspect`
=====

This is a simple web server for viewing/editing data files encoded using
Google Protocol Buffers. Essentially a web interface wrapper around 
`protoc --encode` and `protoc --decode`.

Requires Docker.

### Build it

    docker build -t protobuf-inspect .

### Run it

This tool requires a Docker volume where it can find the "root" of your
`.proto` files. Use this command, replacing `<PROTO_ROOT>` with the
absolute path to where your `.proto` files are found:

    docker run --rm -p 8080:8080 -v <PROTO_ROOT>:/proto-root protobuf-inspect

You can then view the server at `http://localhost:8080`.

By default, `protobuf-inspect` assumes that the file your protobuf message
type is specified in is located at the top level in the volume. If it is
not, you need to specify `-e PROTO_FILE=path/to/your/file.proto`, which
path is relative to `/proto-root` inside the container.

### Use it

The tool requires knowing what message type it is operating on. This is
specified via the URL: `http://localhost:8080/<messageType>`. For example,
the `AddressBook` specified in the [`addressbook.proto`](https://github.com/protocolbuffers/protobuf/blob/master/examples/addressbook.proto)
provided in the protobuf tutorial would correspond to a message type of
`tutorial.AddressBook`, or a URL of `http://localhost:8080/tutorial.AddressBook`.

Load the appropriate URL, then use the interface to:

- Load protobuf-encoded binary data, converting it to [text format](https://developers.google.com/protocol-buffers/docs/reference/cpp/google.protobuf.text_format)
  for human consumption
- Edit it to your pleasure (or write a new one entirely), and save the new
  one back to binary format

That's it. Good luck!
