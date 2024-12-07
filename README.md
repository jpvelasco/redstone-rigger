# Minecraft Server on EKS using AWS CDK

This project deploys a Minecraft server on Amazon EKS (Elastic Kubernetes Service) using AWS CDK (Cloud Development Kit). It provides a scalable and maintainable way to run a Minecraft server in the cloud.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js and npm installed (for CDK CLI)
- Python 3.x installed
- AWS CDK CLI installed (`npm install -g aws-cdk`)
- Docker installed (optional, for local testing)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/jpvelasco/redstone-rigger.git
cd redstone-rigger
```

2. Create and activate a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Deployment

1. Bootstrap your AWS environment for CDK (if you haven't already):
```bash
cdk bootstrap
```

2. Synthesize the CloudFormation template to review changes:
```bash
cdk synth
```

3. Deploy the stack:
```bash
cdk deploy
```

4. After deployment, find your Minecraft server address:
   - Go to the AWS EC2 console
   - Navigate to "Load Balancers" in the left sidebar
   - Find the load balancer created by this stack (named like "MinecraftEks-*")
   - Use the DNS name from the "Description" tab as your Minecraft server address

## Connecting to the Minecraft Server

1. Launch your Minecraft Java Edition client
2. Click "Multiplayer" > "Add Server"
3. Enter a name for your server (e.g., "My EKS Server")
4. For the server address, use:
   ```
   <load-balancer-dns-name>:25565
   ```
   Replace `<load-balancer-dns-name>` with the DNS name from step 4 of Deployment.
5. Click "Done" and connect to your server

## Architecture

This project creates the following AWS infrastructure:
- An Amazon EKS cluster running Kubernetes v1.24+
- A VPC with public and private subnets across multiple Availability Zones
- An EKS managed node group with t3.medium EC2 instances
- A Kubernetes deployment running the official Minecraft server image
- A Kubernetes LoadBalancer service to expose the Minecraft server
- Associated IAM roles and security groups

## Server Configuration

The Minecraft server can be customized through environment variables in the `minecraft_server_manifest.yaml` file. Common settings include:

- `DIFFICULTY`: Set game difficulty (peaceful/easy/normal/hard)
- `MODE`: Gameplay mode (survival/creative/adventure)
- `MOTD`: Server description shown in the client
- `MAX_PLAYERS`: Maximum number of concurrent players
- `MEMORY`: Server memory allocation (default: "2G")
- `ONLINE_MODE`: Enable/disable online mode verification
- `ALLOW_NETHER`: Enable/disable Nether dimension
- `ENABLE_COMMAND_BLOCK`: Enable/disable command blocks

Additional configuration options can be found in the official Minecraft server documentation.

## Cost Considerations

Please be aware of the costs associated with running this infrastructure:
- EKS cluster management fee (~$0.10 per hour)
- EC2 instances in the node group (varies by instance type)
- Load Balancer charges
- Data transfer costs

## Clean Up

To avoid ongoing charges, destroy the resources when not in use:
```bash
cdk destroy
```

## Troubleshooting

1. Server Connection Issues:
   - Verify the security group allows inbound traffic on port 25565
   - Check if the EKS nodes are running: `kubectl get nodes`
   - View pod status: `kubectl get pods`
   - Check pod logs: `kubectl logs deployment/minecraft-server`

2. Performance Issues:
   - Monitor node resources: `kubectl top nodes`
   - Consider adjusting the server memory allocation
   - Scale the node group if needed

3. Common kubectl Commands:
```bash
kubectl get all                     # View all resources
kubectl describe pod <pod-name>     # Get detailed pod info
kubectl logs <pod-name>            # View pod logs
kubectl exec -it <pod-name> -- sh  # Access pod shell
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.