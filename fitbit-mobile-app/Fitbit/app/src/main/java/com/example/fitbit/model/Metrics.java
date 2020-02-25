package com.example.fitbit.model;

import com.google.gson.*;
import com.orm.SugarRecord;


public class Metrics extends SugarRecord {
    private String metricsDescription;
    private long timestamp;
    private double amount;

    public Metrics(){

    }

    public Metrics(String metricsDescription, long timestamp, double amount) {
        this.metricsDescription = metricsDescription;
        this.timestamp = timestamp;
        this.amount = amount;
    }

    public String getMetricsDescription() {
        return metricsDescription;
    }

    public void setMetricsDescription(String metricsDescription) {
        this.metricsDescription = metricsDescription;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }
    public String toString(){
        String result = new Gson().toJson(this);
        return result;
    }
}
