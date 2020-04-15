CWD    = $(CURDIR)
MODULE = $(notdir $(CWD))

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

.PHONY: all
all: target/debug/guest_os $(MODULE).ini
	$^

target/debug/guest_os: src/*.rs Cargo.toml Makefile
	cargo build
