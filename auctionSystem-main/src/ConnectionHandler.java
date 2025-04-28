import model.CreateRoomRequest;
import model.JoinRoomRequest;
import model.SendMessageRequest;

import java.io.*;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

public class ConnectionHandler implements Runnable {
    private final Socket clientSocket;
    private static final Map<String, AuctionRoom> rooms = new HashMap<>();

    public ConnectionHandler(Socket clientSocket) {
        this.clientSocket = clientSocket;
    }

    @Override
    public void run() {
        try (
                ObjectOutputStream out = new ObjectOutputStream(clientSocket.getOutputStream());
                ObjectInputStream in = new ObjectInputStream(clientSocket.getInputStream())
        ) {
            while (true) {
                Object request = in.readObject();
                Object response = processRequest(request, out);
                out.writeObject(response);
                out.flush();
            }
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    private Object processRequest(Object request, ObjectOutputStream out) {
        if (request instanceof CreateRoomRequest) {
            CreateRoomRequest createRoomRequest = (CreateRoomRequest) request;
            String roomNumber = createRoomRequest.getRoomNumber();

            if (!rooms.containsKey(roomNumber)) {
                rooms.put(roomNumber, new AuctionRoom(roomNumber));
                return "Room " + roomNumber + " created successfully.";
            } else {
                return "Room " + roomNumber + " already exists.";
            }
        } else if (request instanceof JoinRoomRequest) {
            JoinRoomRequest joinRoomRequest = (JoinRoomRequest) request;
            String roomNumber = joinRoomRequest.getRoomNumber();

            AuctionRoom room = rooms.get(roomNumber);
            if (room != null) {
                room.addClient(out);
                return "Joined room " + roomNumber + ".";
            } else {
                return "Room " + roomNumber + " does not exist.";
            }
        } else if (request instanceof SendMessageRequest) {
            SendMessageRequest sendMessageRequest = (SendMessageRequest) request;
            String roomNumber = sendMessageRequest.getRoomNumber();
            String message = sendMessageRequest.getMessage();

            AuctionRoom room = rooms.get(roomNumber);
            if (room != null && room.hasClient(out)) {
                room.broadcastMessage(message);
                return "Message sent to room " + roomNumber + ".";
            } else {
                return "You are not a member of room " + roomNumber + ".";
            }
        }

        return "Invalid request.";
    }

}

