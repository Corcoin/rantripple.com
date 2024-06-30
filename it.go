package main

import (
	"fmt"
	"io"
	"net"
	"net/http"
)

func main() {
	port := ":8888" // Port to listen on
	fmt.Printf("Proxy server started on port %s\n", port)

	// Start proxy server
	listener, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Printf("Error starting server: %v\n", err)
		return
	}

	for {
		client, err := listener.Accept()
		if err != nil {
			fmt.Printf("Error accepting connection: %v\n", err)
			continue
		}
		go handleClient(client)
	}
}

func handleClient(client net.Conn) {
	defer client.Close()

	// Read client's request
	request, err := http.ReadRequest(bufio.NewReader(client))
	if err != nil {
		fmt.Printf("Error reading request: %v\n", err)
		return
	}

	// Print request details (optional)
	fmt.Printf("Request received: %s %s\n", request.Method, request.URL)

	// Connect to destination server
	server, err := net.Dial("tcp", request.URL.Host)
	if err != nil {
		fmt.Printf("Error connecting to server: %v\n", err)
		return
	}
	defer server.Close()

	// Forward client's request to server
	err = request.Write(server)
	if err != nil {
		fmt.Printf("Error forwarding request: %v\n", err)
		return
	}

	// Copy server's response back to client
	_, err = io.Copy(client, server)
	if err != nil {
		fmt.Printf("Error copying response: %v\n", err)
		return
	}

	fmt.Println("Request processed successfully")
}
