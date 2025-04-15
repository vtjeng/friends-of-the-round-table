CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra
TARGET = heuristic_search
SRC = heuristic_search.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET) *.o
