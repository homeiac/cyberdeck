#!/usr/bin/expect

# Define the Bluetooth device MAC address
set device_mac "XX:XX:XX:XX:XX:XX"  # Replace with your keyboard's MAC address
set max_retries 3

# Start bluetoothctl
spawn bluetoothctl

# Wait for the prompt
expect -re {^\[bluetooth\]#}

# Check if the device is connected and bonded
send "info $device_mac"
expect {
    -re {Connected:\s+yes.*Bonded:\s+yes} {
        puts "Device $device_mac is connected and bonded. Exiting..."
        send "quit"
        expect eof
        exit 0
    }
    -re {Connected:\s+yes.*Bonded:\s+no} {
        puts "Device $device_mac is connected but not bonded. Proceeding with pairing..."
    }
    -re {Connected:\s+no.*Bonded:\s+yes} {
        puts "Device $device_mac is bonded but not connected. Attempting to connect..."
        send "connect $device_mac"
        expect {
            -re {Connection successful} {
                puts "Device $device_mac connected successfully."
                send "quit"
                expect eof
                exit 0
            }
            timeout {
                puts "Failed to connect to $device_mac. Retrying with remove-pair process..."
            }
        }
    }
    -re {Connected:\s+no.*Bonded:\s+no} {
        puts "Device $device_mac is neither connected nor bonded. Proceeding with pairing..."
    }
    timeout {
        puts "Failed to retrieve device status. Proceeding with reinitialization..."
    }
}

# Remove the device if necessary
send "remove $device_mac"
expect {
    -re {Device has been removed} {puts "Removed device $device_mac successfully."}
    -re {not available} {puts "Device $device_mac not found for removal. Proceeding..."}
}

# Enable the agent
send "agent on"
expect {
    -re {Agent registered} {puts "Agent registered successfully"}
    -re {Failed to register agent} {puts "Agent registration failed"; exit 1}
}

# Set the agent as default
send "default-agent"
expect {
    -re {Default agent request successful} {puts "Default agent set successfully"}
    -re {No agent is registered} {puts "Failed to set default agent"; exit 1}
}

# Scan for the device
send "scan on"
expect {
    -re "$device_mac" {puts "Found device $device_mac"}
    timeout {puts "Failed to find device $device_mac"; exit 1}
}

# Pair the device with retries
for {set i 1} {$i <= $max_retries} {incr i} {
    puts "Attempting to pair with $device_mac (Attempt $i/$max_retries)..."
    send "pair $device_mac"
    expect {
        -re {Pairing successful} {
            puts "Device $device_mac paired successfully."
            break
        }
        -re {Authentication failed} {
            puts "Pairing failed: Authentication error. Retrying..."
        }
        timeout {
            puts "Pairing failed: Timeout. Retrying..."
        }
    }
}

# Trust the device
send "trust $device_mac"
expect {
    -re {Trusted: yes} {puts "Device $device_mac Trusted: yes"}
    timeout {puts "Trusting device $device_mac failed"; exit 1}
}

# Connect to the device
send "connect $device_mac"
expect {
    -re {Connection successful} {
        puts "Device $device_mac connected successfully."
    }
    timeout {
        puts "Final attempt to connect $device_mac failed."
        exit 1
    }
}

# Stop scanning
send "scan off"
expect -re {^\[bluetooth\]#}

# Exit bluetoothctl
send "quit"
expect eof
