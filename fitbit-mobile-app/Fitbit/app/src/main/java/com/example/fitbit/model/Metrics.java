package com.example.fitbit.model;

import com.orm.SugarRecord;

import java.util.Date;

public class Metrics extends SugarRecord {
    private MetricsDescription metricsDescription;
    private Date timestamp;
    private double amount;

    public Metrics(){

    }

    public Metrics(MetricsDescription metricsDescription, Date timestamp, double amount) {
        this.metricsDescription = metricsDescription;
        this.timestamp = timestamp;
        this.amount = amount;
    }

    public MetricsDescription getMetricsDescription() {
        return metricsDescription;
    }

    public void setMetricsDescription(MetricsDescription metricsDescription) {
        this.metricsDescription = metricsDescription;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }
}
