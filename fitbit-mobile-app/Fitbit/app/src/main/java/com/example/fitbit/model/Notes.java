package com.example.fitbit.model;

import com.orm.SugarRecord;

import java.util.Date;

public class Notes extends SugarRecord {

    private String note;
    private Date timestamp;

    public Notes() {
    }

    public Notes(String note, Date timestamp) {
        this.note = note;
        this.timestamp = timestamp;
    }

    public String getNote() {
        return note;
    }

    public void setNote(String note) {
        this.note = note;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }
}
