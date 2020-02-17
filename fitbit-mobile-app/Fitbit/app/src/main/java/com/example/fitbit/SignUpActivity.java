package com.example.fitbit;

import android.content.Intent;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;


import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;


public class SignUpActivity extends AppCompatActivity {
    private static final String TAG = "SignupActivity";
    EditText username;
    EditText password;
    EditText rePassword;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);
        username=findViewById(R.id.editTextUsernameSignUp);
        password=findViewById(R.id.editTextPasswordSignUp);
        rePassword=findViewById(R.id.editTextRePasswordSignUp);
        findViewById(R.id.buttonSignUp).setOnClickListener((view)->{
            if(username.getText().toString().trim().equals("")){
                username.setError("You must provide a username");
                return;
            }else if(password.getText().toString().equals("")){
                password.setError("You must provide a password");
                return;
            }else if(!password.getText().toString().equals(rePassword.getText().toString())){
                rePassword.setError("Password are not matching");
                return;
            }
            CallAPI request=new CallAPI("POST", output -> {
                try {
                    JSONObject obj = new JSONObject(output);
                    if(obj.has("error")){
                        if(obj.getString("error").equals("username already exists")){
                            username.setError("Username already exists");
                        }
                        else {
                            Toast.makeText(SignUpActivity.this,obj.getString("error"),Toast.LENGTH_SHORT).show();
                        }
                    }else if(obj.has("status")){
                        Intent myIntent = new Intent(SignUpActivity.this, MainActivity.class);
                        startActivity(myIntent);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }

            });
            //String params = String.format("{\"username\":\"%s\",\"password\":\"%s\",\"repeat_password\":\"%s\"}",username.getText().toString(),password.getText().toString(),rePassword.getText().toString());

            request.execute(Urls.SERVER_URL+Urls.SIGNUP_ENDPOINT,"username",username.getText().toString(),"password",password.getText().toString(),"repeat_password",rePassword.getText().toString());
        });

        findViewById(R.id.textViewLogin).setOnClickListener((view)->{
            Intent myIntent= new Intent(SignUpActivity.this,LoginActivity.class);
            startActivity(myIntent);
        });

    }


}
