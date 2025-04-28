package model;

import java.io.Serializable;

public class JoinRoomRequest implements Serializable {
    private final String roomNumber;

    public JoinRoomRequest(String roomNumber) {
        this.roomNumber = roomNumber;
    }

    public String getRoomNumber() {
        return roomNumber;
    }
}
