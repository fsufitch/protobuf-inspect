FROM alpine:latest AS unpack-vendor

ENV PROTO_VERSION_SEMVER=3.7.0rc2
ENV PROTO_VERSION_FILE=3.7.0-rc-2

RUN apk add unzip

ADD https://github.com/protocolbuffers/protobuf/releases/download/v${PROTO_VERSION_SEMVER}/protoc-${PROTO_VERSION_FILE}-linux-x86_64.zip /protoc/protoc.zip
RUN unzip /protoc/protoc.zip -d /protoc
RUN rm /protoc/protoc.zip /protoc/readme.txt

#======

FROM python:3.7-alpine

VOLUME [ "/proto-root" ]

COPY --from=unpack-vendor /protoc /usr/local
RUN apk add bash gcompat libc6-compat libatomic gcc libc-dev linux-headers
RUN pip install flask uwsgi

ENV PROTO_ROOT="/proto-root"
ENV PROTO_FILE="/proto-root/*.proto"

WORKDIR /app

ADD static static
ADD uwsgi.ini .
ADD webserver.py .

ENTRYPOINT [ "uwsgi", "--ini", "uwsgi.ini"]