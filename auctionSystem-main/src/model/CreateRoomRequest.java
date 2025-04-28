package model;

import java.io.Serializable;

public class CreateRoomRequest implements Serializable {
    private final String roomNumber;

    public CreateRoomRequest(String roomNumber) {
        this.roomNumber = roomNumber;
    }

    public String getRoomNumber() {
        return roomNumber;
    }
}
