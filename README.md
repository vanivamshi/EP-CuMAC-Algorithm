# EP-CuMAC-Algorithm

Developed as a part of my Ph.D. research, accessible at - https://doi.org/10.1016/j.iot.2023.101004

Each of the folder contains programs for different functions performed by the EP-CuMAC algorithm.
1) SINR - Measures SINR at the server aend and sends a feedback in case of low SINR
2) Delay - Measures packet delay at the server aend and sends a feedback in case of high packet delay
3) Packet drop_probability - In case of dropped auhtentication tags, probability of tag reception is calculated based on received tags to auhtneticate the messages
4) Message prediction using ML - Predict lost messages using ML
5) Msg merge_retransmission - In case where all packets are lost, messages and authentication tags of lost messages are merged with those to be transmitted in the upcoming transmission and then trannsmitted

File nomenclature:
1) client_X.py - client file common to both real-time and full authentication
2) server_X_full - server file for full authentication
3) server_X_realtime - server file for realtime authentication
