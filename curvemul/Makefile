# You can change this to release|memcheck|verbose|static|allwarn
BUILD = release

# Settings for folders
OBJECT_DIR  = obj
LIBRARY_DIR = src
SOURCE_DIR  = src
SHARED_DIR  = so

# Compilers options
CC              = g++
CFLAGS.release  = -I$(LIBRARY_DIR) -O2
CFLAGS.allwarn  = -I$(LIBRARY_DIR) -O2 -Wall -Wextra -Wpedantic
CFLAGS.memcheck = -I$(LIBRARY_DIR) -O0 -ggdb -fsanitize=address
CFLAGS.verbose  = -I$(LIBRARY_DIR) -O2 -ggdb -D DLOG_VERBOSE=1
CFLAGS.static   = -I$(LIBRARY_DIR) -O2 -static
CFLAGS          = $(CFLAGS.$(BUILD))
LIBS            = -lntl

# Requirements and stuffs
FULLDEPS := $(shell find $(LIBRARY_DIR) -name '*.h')
FULLOBJS := $(shell find $(SOURCE_DIR) -name '*.cpp' | sed -e "s/^$(SOURCE_DIR)/$(OBJECT_DIR)/" | sed -e "s/\\.cpp$$/.o/")

# Default targets
default: test libcurvemul

# For creating a user interface binary
test: $(FULLOBJS) $(OBJECT_DIR)/test.o
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)
	strip test

$(OBJECT_DIR):
	mkdir -p $(OBJECT_DIR)

$(OBJECT_DIR)/%.o: $(SOURCE_DIR)/%.cpp $(FULLDEPS) | $(OBJECT_DIR)
	$(CC) -fPIC -c -o $@ $< $(CFLAGS)

# For commands
.PHONY: clean libcurvemul
clean:
	rm -f $(SOURCE_DIR)/*.o $(OBJECT_DIR)/*.o $(SHARED_DIR)/*.so ./test

# For creating shared library :)
libcurvemul: $(SHARED_DIR)/libcurvemul.so

$(SHARED_DIR)/libcurvemul.so: $(FULLOBJS) | $(SHARED_DIR)
	$(CC) -shared -o $@ $^ $(CFLAGS) $(LIBS)

$(SHARED_DIR):
	mkdir -p $(SHARED_DIR)