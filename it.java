import java.io.*;
import java.net.*;

public class SimpleProxyServer {
    public static void main(String[] args) throws IOException {
        int port = 8888; // Port to listen on
        ServerSocket listener = new ServerSocket(port);
        System.out.println("Proxy server started on port " + port);

        while (true) {
            Socket client = listener.accept();
            new Thread(() -> handleClient(client)).start(); // Handle client request in a separate thread
        }
    }

    private static void handleClient(Socket client) {
        try (
            InputStream clientIn = client.getInputStream();
            OutputStream clientOut = client.getOutputStream();
        ) {
            Socket server = new Socket("example.com", 80); // Connect to destination server (example.com:80)
            InputStream serverIn = server.getInputStream();
            OutputStream serverOut = server.getOutputStream();

            new Thread(() -> {
                try {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = clientIn.read(buffer)) != -1) {
                        serverOut.write(buffer, 0, bytesRead);
                        serverOut.flush();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }).start();

            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = serverIn.read(buffer)) != -1) {
                clientOut.write(buffer, 0, bytesRead);
                clientOut.flush();
            }

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                client.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
