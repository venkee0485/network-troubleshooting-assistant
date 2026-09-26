from rag import retrieve_relevant_context


test_queries = [
    "Users in VLAN 20 cannot access the internet but VLAN 10 works.",

    "OSPF neighbor is not forming between two Cisco routers.",

    "FortiGate users can reach the LAN gateway but cannot access "
    "the internet. Check firewall policy and NAT.",

    "Traffic between two zones is being denied by a Palo Alto firewall.",

    "Windows Server can ping an IP address but cannot resolve the hostname.",

    "Azure virtual machine cannot accept traffic on TCP port 443. "
    "Check the NSG configuration.",

    "AWS EC2 instance cannot access the internet from a private subnet. "
    "Check route table and NAT Gateway."
]


for query_number, query in enumerate(test_queries, start=1):

    print("\n" + "=" * 70)
    print(f"TEST QUERY {query_number}")
    print("=" * 70)

    print(f"\nUser Query:\n{query}")

    results = retrieve_relevant_context(
        query,
        top_k=3
    )

    print("\nRetrieved Knowledge:\n")

    for number, result in enumerate(results, start=1):

        print(f"--- Result {number} ---")
        print(f"Source: {result['source']}")
        print(
            f"Similarity Score: "
            f"{result['score']:.4f}"
        )
        print(result["content"])
        print()