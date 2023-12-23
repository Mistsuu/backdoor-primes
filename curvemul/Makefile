# You can change this to release|memcheck|verbose|static|allwarn
BUILD = release

# Settings for folders
OBJECT_DIR  = obj
LIBRARY_DIR = src libs/progressbar/include/progressbar
SOURCE_DIR  = src
SHARED_DIR  = so
EXTERNAL_OBJS = libs/progressbar/libprogressbar.so

# Automatic modification here
LIBRARY_CFG = $(patsubst %, -I%, $(LIBRARY_DIR))

# Compilers options
CC              = g++
CFLAGS.release  = $(LIBRARY_CFG) -O2
CFLAGS.allwarn  = $(LIBRARY_CFG) -O2 -Wall -Wextra -Wpedantic
CFLAGS.memcheck = $(LIBRARY_CFG) -O0 -ggdb -fsanitize=address
CFLAGS.verbose  = $(LIBRARY_CFG) -O2 -ggdb -D DLOG_VERBOSE=1
CFLAGS.static   = $(LIBRARY_CFG) -O2 -static
CFLAGS          = $(CFLAGS.$(BUILD))
LIBS            = -lntl -lncurses

# Requirements and stuffs
FULLDEPS := $(shell find $(LIBRARY_DIR) -name '*.h')
FULLOBJS := $(shell find $(SOURCE_DIR) -name '*.cpp' | sed -e "s/^$(SOURCE_DIR)/$(OBJECT_DIR)/" | sed -e "s/\\.cpp$$/.o/")

# Default targets
default: test libcurvemul

# For creating a user interface binary
test: $(FULLOBJS) $(OBJECT_DIR)/test.o $(EXTERNAL_OBJS)
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
	cd libs/progressbar && make clean

# For creating shared library :)
libcurvemul: $(SHARED_DIR)/libcurvemul.so $(EXTERNAL_OBJS)

$(SHARED_DIR)/libcurvemul.so: $(FULLOBJS) $(EXTERNAL_OBJS) | $(SHARED_DIR)
	$(CC) -shared -o $@ $^ $(CFLAGS) $(LIBS)

$(SHARED_DIR):
	mkdir -p $(SHARED_DIR)

# ============================= customize for external libraries ==================================
$(EXTERNAL_OBJS):
    # Builiding for libprogressbar
	cd libs/progressbar && make