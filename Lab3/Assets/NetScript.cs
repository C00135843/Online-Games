using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Collections.Generic;

public class NetScript : MonoBehaviour {

    int socketId;
    int socketPort = 8888;
    int myChannelId;
    int connectionId;
    int count;
    //your_updateMessage list: 
    private List<byte> _updateMessage = new List<byte> { };
    // Use this for initialization
    void Start () {

        NetworkTransport.Init();
        ConnectionConfig config = new ConnectionConfig();
        myChannelId = config.AddChannel(QosType.Reliable);

        int maxConnections = 5;
        HostTopology topology = new HostTopology(config, maxConnections);
        socketId = NetworkTransport.AddHost(topology, socketPort);
        Debug.Log("Socket Open. SocketId is: " + socketId);
    }
	
	// Update is called once per frame
	void Update () {
        int recHostId;
        int recConnectionId;
        int recChannelId;
        byte[] recBuffer = new byte[1024];
        int bufferSize = 1024;
        int dataSize;
        byte error;
        NetworkEventType recNetworkEvent = NetworkTransport.Receive(out recHostId, out recConnectionId, out recChannelId, recBuffer, bufferSize, out dataSize, out error);

        switch (recNetworkEvent)
        {
            case NetworkEventType.Nothing:
                break;
            case NetworkEventType.ConnectEvent:
                Debug.Log("incoming connection event received");
                break;
            case NetworkEventType.DataEvent:
                Stream stream = new MemoryStream(recBuffer);
                BinaryFormatter formatter = new BinaryFormatter();
                byte[] message = formatter.Deserialize(stream) as byte[];
                receiveMessage(message, message.Length, "TEST");
                Debug.Log("incoming message event received: " + message);
                break;
            case NetworkEventType.DisconnectEvent:
                Debug.Log("remote client event disconnected");
                break;
        }

    }

    public void SendMyUpdate(float posX, float posY,Vector2 velocity, float rotZ )
    {
        _updateMessage.Clear();
        _updateMessage.Add((byte)'U');
        _updateMessage.AddRange(System.BitConverter.GetBytes(posX));
        _updateMessage.AddRange(System.BitConverter.GetBytes(posY));
        _updateMessage.AddRange(System.BitConverter.GetBytes(velocity.x));
        _updateMessage.AddRange(System.BitConverter.GetBytes(velocity.y));
        _updateMessage.AddRange(System.BitConverter.GetBytes(rotZ));
        byte[] messageToSend = _updateMessage.ToArray();
        Debug.Log("Sending my update message  " + messageToSend + " to all players in the room");
        //PlayGamesPlatform.Instance.RealTime.SendMessageToAll(false, messageToSend);
    }
    public void receiveMessage(byte[] data, int _updateMessageLength, string senderId)
    {
        char messageType = (char)data[1];
        if (messageType == 'U' && data.Length == _updateMessageLength) {
            float posX = System.BitConverter.ToSingle(data, 2);
            float posY = System.BitConverter.ToSingle(data, 6);
            float velX = System.BitConverter.ToSingle(data, 10);
            float velY = System.BitConverter.ToSingle(data, 14);
            float rotZ = System.BitConverter.ToSingle(data, 18);
            Debug.Log("Player " + senderId + " is at (" + posX + ", " + posY + ") traveling (" + velX + ", " + velY + ") rotation " + rotZ);
            
        }
    }
    public void Connect()
    {
        byte error;
        connectionId = NetworkTransport.Connect(socketId, "149.153.102.52", socketPort, 0, out error);
        Debug.Log("Connected to server. connectionId: " + connectionId);

    }

    public void SendSocketMessage()
    {
        byte error;
        byte[] buffer = new byte[1024];
        Stream stream = new MemoryStream(buffer);
        BinaryFormatter formatter = new BinaryFormatter();
        formatter.Serialize(stream, "Hello jonnie");

        int bufferSize = 1024;

        NetworkTransport.Send(socketId, connectionId, myChannelId, buffer, bufferSize, out error);
    }


}
