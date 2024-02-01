# Information
Full Name: Mohammad Amin Karami

Student ID: 98105998

# How to Run the Code
The project is written in Python. To execute the code, simply run the following command in the console:

```bash
make run-server
```

Additionally, to clean up the virtual environment, you can run the following command in the console:

```bash
make clean
```

# Code Description
The implementation is located in the `src` directory.

In the `dns_database.py` file, there is a class responsible for reading from the `/etc/myhosts` file and storing the records related to the IP of each host in a dictionary. For example, for the record:

93.184.216.34 example.com

The dictionary will look like this:

```py
data = {
    "example.com": "93.184.216.34"
}
```

You can retrieve the IP address of a host using the `get_ip_of_domain` function if it exists.

The `dns_server.py` file contains the implementation of the server, which is implemented in parallel using the `async.io` library.

Packet handling implementation for the DNS server is done in `dns_packet`.

The `Serializable` class is an interface for classes that require `parse` and `pack` methods, and this class is inherited by sections and the `DNSPacket` itself.

Each packet has 5 sections, and each section is implemented in the `sections` directory.

The `DNSPacket` class uses these sections and uses the `parse` and `pack` methods of each section for parsing and packing.

The `helpers.py` file contains functions that make data extraction and creation easier. For example, the `convert_number_to_bit_string` function allows converting a number into a bit sequence of a specified length.

The `constants.py` file contains Enums such as `RType`, which improves code readability.

In the `sections` directory, each section related to the packet is implemented. Since `Answer`, `Authority`, and `Additional` are all of type RR, an `RR` class is also implemented, and these sections inherit from it.