package model;

import java.io.Serializable;

public class SendMessageRequest implements Serializable {
    private final String roomNumber;
    private final String message;

    public SendMessageRequest(String roomNumber, String message) {
        this.roomNumber = roomNumber;
        this.message = message;
    }

    public String getRoomNumber() {
        return roomNumber;
    }

    public String getMessage() {
        return message;
    }
}
