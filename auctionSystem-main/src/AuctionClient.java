import model.CreateRoomRequest;
import model.JoinRoomRequest;
import model.SendMessageRequest;

import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class AuctionClient {
    private static final String SERVER_ADDRESS = "localhost";
    private static final int PORT = 12345;

    public static void main(String[] args) {
        try (
                Socket socket = new Socket(SERVER_ADDRESS, PORT);
                ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
                ObjectInputStream in = new ObjectInputStream(socket.getInputStream())
        ) {
            System.out.println("Connected to server.");

            Scanner scanner = new Scanner(System.in);
            String choice;

            do {
                System.out.println("Choose an option:");
                System.out.println("1. Create a new auction room");
                System.out.println("2. Join an existing auction room");
                System.out.println("3. Send message to an auction room");
                System.out.println("4. Exit");
                choice = scanner.nextLine();

                switch (choice) {
                    case "1":
                        System.out.println("Enter room number:");
                        String roomNumber = scanner.nextLine();
                        out.writeObject(new CreateRoomRequest(roomNumber));
                        out.flush();
                        System.out.println(in.readObject());
                        break;
                    case "2":
                        System.out.println("Enter room number:");
                        roomNumber = scanner.nextLine();
                        out.writeObject(new JoinRoomRequest(roomNumber));
                        out.flush();
                        System.out.println(in.readObject());
                        break;
                    case "3":
                        System.out.println("Enter room number:");
                        roomNumber = scanner.nextLine();
                        System.out.println("Enter message:");
                        String message = scanner.nextLine();
                        out.writeObject(new SendMessageRequest(roomNumber, message));
                        out.flush();
                        System.out.println(in.readObject());
                        break;
                    case "4":
                        System.out.println("Exiting...");
                        break;
                    default:
                        System.out.println("Invalid option. Please try again.");
                        break;
                }

            } while (!choice.equals("4"));

        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
