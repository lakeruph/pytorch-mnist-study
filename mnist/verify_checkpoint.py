import torch
from main import Net
from torchvision import datasets, transforms

new_model = Net()

state = torch.load(
    'mnist_cnn_baseline_e3.pt',
    map_location='cpu',
    weights_only=True
)
new_model.load_state_dict(state)
new_model.eval()

print("模型权重加载成功!")

transform=transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
    ])
dataset = datasets.MNIST('../data', train=False, download=True,transform=transform)
test_loader = torch.utils.data.DataLoader(dataset, batch_size=1000, shuffle=False)

with torch.inference_mode():
    correct = 0
    for images, targets in test_loader:
        outputs = new_model(images)
        pred = outputs.argmax(dim=1)
        correct += (pred == targets).sum().item()

print("Total samples:{}".format(len(dataset)))
print("Correct predictions:{}".format(correct))
print("Accuracy:{}%".format(correct/len(dataset)*100))