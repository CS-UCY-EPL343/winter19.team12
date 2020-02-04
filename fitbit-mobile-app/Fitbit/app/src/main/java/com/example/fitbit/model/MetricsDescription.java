package com.example.fitbit.model;

import com.orm.SugarRecord;

public class MetricsDescription extends SugarRecord {
    private String description;

    public MetricsDescription(){

    }

    public MetricsDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}