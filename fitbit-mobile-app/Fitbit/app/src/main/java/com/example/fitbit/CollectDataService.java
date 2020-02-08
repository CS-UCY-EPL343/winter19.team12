package com.example.fitbit;

import android.content.Intent;
import android.os.IBinder;
import android.app.Service;
import android.util.Log;

import androidx.annotation.Nullable;

public class CollectDataService extends Service {
    private Nano mNano;
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // do your jobs here
        Log.d("service","started service");
        try {
            mNano = new Nano(5000);
        }
        catch(Exception e){
            e.printStackTrace();
        }
        super.onStartCommand(intent, flags, startId);
        return START_STICKY;
    }
}