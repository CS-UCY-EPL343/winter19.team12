package com.example.fitbit;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.EditText;
import android.widget.RadioButton;

public class EditProfile extends AppCompatActivity {
    private final String EDIT_PROFILE_ENDPOINT="/edit_profile_api";
    private EditText password;
    private EditText rePassword;
    private EditText name;
    private EditText surname;
    private EditText birthday;
    private EditText height;
    private RadioButton isMale;
    private RadioButton isFemale;
    private EditText email;
    private EditText phone;
    private EditText address;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_profile);
        password=findViewById(R.id.editTextPasswordEditProfile);
        rePassword=findViewById(R.id.editTextRePasswordEditProfile);
        name=findViewById(R.id.editTextNameEditProfile);
        surname=findViewById(R.id.editTextSurnameEditProfile);
        birthday=findViewById(R.id.editTextBirthdayEditProfile);
        height=findViewById(R.id.editTextHeightEditProfile);
        isMale=findViewById(R.id.radioButtonIsMaleEditProfile);
        isFemale=findViewById(R.id.radioButtonIsFemaleEditProfile);
        email=findViewById(R.id.editTextEmailEditProfile);
        phone=findViewById(R.id.editTextTelephoneEditProfile);
        address=findViewById(R.id.editTextAddressEditProfile);
    }
}
