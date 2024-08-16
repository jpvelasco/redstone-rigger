# Minecraft Server on EKS using CDK

This project deploys a Minecraft server on Amazon EKS using AWS CDK.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js and npm installed
- Python 3.x installed
- AWS CDK CLI installed (`npm install -g aws-cdk`)

## Setup

1. Clone the repository:
git clone https://github.com/jpvelasco/redstone-rigger.git
cd redstone-rigger


2. Create a virtual environment:
python3 -m venv .venv
source .venv/bin/activate # On Windows use .venv\Scripts\activate


3. Install dependencies:
pip install -r requirements.txt



## Deployment

1. Synthesize the CloudFormation template:
cdk synth


2. Deploy the stack:
cdk deploy


3. After deployment, find your Minecraft server address:
- Go to the AWS EC2 console
- Navigate to "Load Balancers" in the left sidebar
- Find the load balancer created by this stack
- Use the DNS name in the "Description" tab as your Minecraft server address

## Connecting to the Minecraft Server

1. Open your Minecraft client
2. Go to Multiplayer > Add Server
3. Enter a name for your server
4. For the server address, use:

    load-balancer-dns-name:25565

    Note: Replace `load-balancer-dns-name` with the DNS name from step 3 of Deployment.

5. Click "Done" and connect to your server

## Architecture

This project sets up the following AWS resources:
- An Amazon EKS cluster
- A VPC with public and private subnets
- An EKS managed node group with 2 EC2 instances
- A Kubernetes deployment running the Minecraft server
- A Kubernetes service of type LoadBalancer to expose the server

## Customization

You can customize the Minecraft server by modifying the environment variables in the `minecraft_eks_cdk_stack.py` file. Refer to the [itzg/minecraft-server](https://github.com/itzg/docker-minecraft-server) Docker image documentation for available options.

## Clean Up

To avoid incurring future charges, remember to destroy the resources:
cdk destroy


## Troubleshooting

- If you can't connect to the server, ensure that your EKS cluster's security group allows inbound traffic on port 25565.
- Check the status of your Kubernetes pods and services using `kubectl` commands.
- Review the CloudFormation events in the AWS Console for any deployment issues.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.