package com.datacoin.android;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends AppCompatActivity {
    
    private static final int PERMISSION_REQUEST_CODE = 1001;
    private TextView statusText;
    private Button startServerButton;
    private Button openWebInterfaceButton;
    private Button createWalletButton;
    private Button mineBlockButton;
    private DataCoinCore dataCoinCore;
    private Handler uiHandler;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initializeViews();
        setupPermissions();
        initializeDataCoin();
        setupClickListeners();
        
        uiHandler = new Handler();
    }
    
    private void initializeViews() {
        statusText = findViewById(R.id.statusText);
        startServerButton = findViewById(R.id.startServerButton);
        openWebInterfaceButton = findViewById(R.id.openWebInterfaceButton);
        createWalletButton = findViewById(R.id.createWalletButton);
        mineBlockButton = findViewById(R.id.mineBlockButton);
        
        statusText.setText("🪙 DataCoin Android Edition\nInitializing...");
    }
    
    private void setupPermissions() {
        String[] permissions = {
            Manifest.permission.INTERNET,
            Manifest.permission.ACCESS_NETWORK_STATE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WAKE_LOCK
        };
        
        boolean allPermissionsGranted = true;
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                allPermissionsGranted = false;
                break;
            }
        }
        
        if (!allPermissionsGranted) {
            ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE);
        }
    }
    
    private void initializeDataCoin() {
        dataCoinCore = new DataCoinCore(this);
        dataCoinCore.initialize(new DataCoinCore.InitializationCallback() {
            @Override
            public void onSuccess() {
                runOnUiThread(() -> {
                    statusText.setText("✅ DataCoin initialized successfully!\n" +
                                     "🔗 Blockchain ready\n" +
                                     "💼 Wallet system ready\n" +
                                     "🌐 Data converter ready");
                    enableButtons();
                });
            }
            
            @Override
            public void onError(String error) {
                runOnUiThread(() -> {
                    statusText.setText("❌ Initialization failed:\n" + error);
                    showToast("Failed to initialize DataCoin: " + error);
                });
            }
        });
    }
    
    private void enableButtons() {
        startServerButton.setEnabled(true);
        openWebInterfaceButton.setEnabled(false); // Enable after server starts
        createWalletButton.setEnabled(true);
        mineBlockButton.setEnabled(true);
    }
    
    private void setupClickListeners() {
        startServerButton.setOnClickListener(v -> startDataCoinServer());
        openWebInterfaceButton.setOnClickListener(v -> openWebInterface());
        createWalletButton.setOnClickListener(v -> createWallet());
        mineBlockButton.setOnClickListener(v -> startMining());
    }
    
    private void startDataCoinServer() {
        startServerButton.setEnabled(false);
        statusText.setText("🚀 Starting DataCoin server...");
        
        dataCoinCore.startServer(new DataCoinCore.ServerCallback() {
            @Override
            public void onServerStarted(int port) {
                runOnUiThread(() -> {
                    statusText.setText("✅ DataCoin server running!\n" +
                                     "🌐 Port: " + port + "\n" +
                                     "📱 Access: http://localhost:" + port + "\n" +
                                     "🔗 Ready for connections");
                    openWebInterfaceButton.setEnabled(true);
                    startServerButton.setText("Server Running");
                });
            }
            
            @Override
            public void onServerError(String error) {
                runOnUiThread(() -> {
                    statusText.setText("❌ Server failed to start:\n" + error);
                    startServerButton.setEnabled(true);
                    showToast("Server error: " + error);
                });
            }
        });
    }
    
    private void openWebInterface() {
        Intent intent = new Intent(this, WebInterfaceActivity.class);
        intent.putExtra("server_port", dataCoinCore.getServerPort());
        startActivity(intent);
    }
    
    private void createWallet() {
        dataCoinCore.createWallet("android_wallet_" + System.currentTimeMillis(), 
            new DataCoinCore.WalletCallback() {
                @Override
                public void onWalletCreated(String walletName, String address) {
                    runOnUiThread(() -> {
                        showToast("Wallet created: " + walletName);
                        statusText.setText(statusText.getText() + "\n💼 Wallet: " + walletName);
                    });
                }
                
                @Override
                public void onWalletError(String error) {
                    runOnUiThread(() -> showToast("Wallet creation failed: " + error));
                }
            });
    }
    
    private void startMining() {
        mineBlockButton.setEnabled(false);
        mineBlockButton.setText("Mining...");
        
        dataCoinCore.startMining(new DataCoinCore.MiningCallback() {
            @Override
            public void onBlockMined(int blockIndex, double reward) {
                runOnUiThread(() -> {
                    showToast("Block " + blockIndex + " mined! Reward: " + reward + " DC");
                    mineBlockButton.setEnabled(true);
                    mineBlockButton.setText("Mine Block");
                    statusText.setText(statusText.getText() + "\n⛏️ Mined block " + blockIndex);
                });
            }
            
            @Override
            public void onMiningError(String error) {
                runOnUiThread(() -> {
                    showToast("Mining failed: " + error);
                    mineBlockButton.setEnabled(true);
                    mineBlockButton.setText("Mine Block");
                });
            }
        });
    }
    
    private void showToast(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            boolean allGranted = true;
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false;
                    break;
                }
            }
            
            if (!allGranted) {
                showToast("Some permissions were denied. DataCoin may not work properly.");
            }
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (dataCoinCore != null) {
            dataCoinCore.cleanup();
        }
    }
}