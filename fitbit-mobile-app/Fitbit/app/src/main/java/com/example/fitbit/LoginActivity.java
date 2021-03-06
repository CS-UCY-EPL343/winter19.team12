package com.example.fitbit;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.app.AlertDialog;
import android.widget.TextView;

import org.json.*;
import com.example.fitbit.model.User;
import com.orm.SugarRecord;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class LoginActivity extends Activity{
    private static String jwt,username;
    private Button mLoginBtn;
    private boolean loginSuccess=false;
    private EditText mPasswordInput,mUsernameInput;
    private TextView registerText;

    @Override
    public void onCreate(Bundle bundle){
        super.onCreate(bundle);
        setContentView(R.layout.login);
        if(User.count(User.class,null,null)>=1){
            Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
            startActivity(myIntent);
        }
        mLoginBtn = (Button)findViewById(R.id.login_button);
        mUsernameInput = (EditText)findViewById(R.id.username_field);
        mPasswordInput = (EditText)findViewById(R.id.password_field);
        registerText = (TextView)findViewById(R.id.textView5);
        registerText.setOnClickListener(v -> {
            Intent myIntent = new Intent(LoginActivity.this, SignUpActivity.class);
            startActivity(myIntent);
        });
        Log.d("TEST","mLoginBtn:"+mLoginBtn);
        mLoginBtn.setOnClickListener(v -> handleLogin(mUsernameInput.getText().toString(),mPasswordInput.getText().toString()));
    }

    /**
     * @brief Sends a post request to the login API endpoint with the username and password
     * and handles the response
     * @param username entered username
     * @param password entered password
     */
    public void handleLogin(String username,String password){
        Log.d("TEST",username.isEmpty()+" "+password.isEmpty());
        if(username.isEmpty() || password.isEmpty()){
            new AlertDialog.Builder(this)
                    .setTitle("Error")
                    .setMessage("Username or password is empty")
                    .show();
            return;
        }
        LoginActivity.username=username;
        //String params = String.format("{\"username\":\"%s\",\"password\":\"%s\"}",username,password);
        CallAPI request = new CallAPI("POST", output -> {
            Log.d("TEST","output:"+output);
            try {
                JSONObject obj = new JSONObject(output);
                String title=null;
                String message = null;
                if(!obj.has("access")){
                    title="Wrong credentials";
                    message="Wrong username or password entered";
                    new AlertDialog.Builder(LoginActivity.this)
                            .setTitle(title)
                            .setMessage(message)
                            .show();
                }
                else{
                    User user = new User(LoginActivity.username,obj.getString("access"));
                    user.save();
                    Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
                    startActivity(myIntent);
                }
            }
            catch(Exception e){
                e.printStackTrace();
            }
        });
        request.execute(Urls.SERVER_URL+Urls.LOGIN_ENDPOINT,"username",username,"password",password);

    }

}
