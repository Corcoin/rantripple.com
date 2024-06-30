using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

class SimpleProxyServer
{
    static async Task Main(string[] args)
    {
        int port = 8888; // Port to listen on
        TcpListener listener = new TcpListener(IPAddress.Any, port);
        listener.Start();
        Console.WriteLine($"Proxy server started on port {port}");

        while (true)
        {
            TcpClient client = await listener.AcceptTcpClientAsync();
            _ = HandleClientAsync(client); // Handle client request asynchronously
        }
    }

    static async Task HandleClientAsync(TcpClient client)
    {
        using (NetworkStream clientStream = client.GetStream())
        {
            using (TcpClient server = new TcpClient())
            {
                await server.ConnectAsync("example.com", 80); // Connect to destination server (example.com:80)

                using (NetworkStream serverStream = server.GetStream())
                {
                    await clientStream.CopyToAsync(serverStream);
                    await serverStream.CopyToAsync(clientStream);
                }
            }
        }
    }
}
