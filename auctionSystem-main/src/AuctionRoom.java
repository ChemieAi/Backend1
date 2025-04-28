import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.HashMap;
import java.util.Map;

public class AuctionRoom {
    private final String roomNumber;
    private final Map<ObjectOutputStream, String> clients = new HashMap<>();

    public AuctionRoom(String roomNumber) {
        this.roomNumber = roomNumber;
    }

    public void addClient(ObjectOutputStream out) {
        clients.put(out, "Client" + clients.size());
    }

    public boolean hasClient(ObjectOutputStream out) {
        return clients.containsKey(out);
    }

    public void broadcastMessage(String message) {
        for (ObjectOutputStream out : clients.keySet()) {
            try {
                out.writeObject("[" + clients.get(out) + "]: " + message);
                out.flush();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
