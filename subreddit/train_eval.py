import time
import torch

eval_accu = []; eval_losses = [];
train_accu = []; train_losses = [];

def evaluate(dataloader, model, criterion):
    model.eval()
    total_acc, total_count = 0, 0 
    
    running_loss = 0
    
    with torch.no_grad():
        for idx, (label, text, offsets) in enumerate(dataloader):
            predicted_label = model(text, offsets)
            loss = criterion(predicted_label, label)
            
            running_loss += loss.item()
            
            total_acc += (predicted_label.argmax(1) == label).sum().item()
            total_count += label.size(0)
    
    test_loss = running_loss / len(dataloader)
    eval_losses.append(test_loss)
    
    eval_accu.append(100 * total_acc/total_count)
    return total_acc/total_count

def train(dataloader, model, criterion, optimizer, epoch):
    model.train()
    total_acc, total_count = 0, 0
    log_interval = 500
    start_time = time.time()
    
    running_loss = 0
    
    for idx, (label, text, offsets) in enumerate(dataloader):
        optimizer.zero_grad()
        predicted_label = model(text, offsets)
        loss = criterion(predicted_label, label)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.1)
        optimizer.step()
        total_acc += (predicted_label.argmax(1) == label).sum().item()
        total_count += label.size(0)
        
        running_loss += loss.item()
        
        if idx % log_interval == 0 and idx > 0:
            elased = time.time() - start_time 
            print('| epoch {:3d} | {:5d}/{:5d} batches '
                  '| accuracy {:8.3f}'.format(epoch, idx, len(dataloader), total_acc/total_count))
            total_acc, total_count = 0, 0
            start_time = time.time()
            
        train_loss = running_loss / len(dataloader)
        train_losses.append(train_loss)
        
        train_accu.append(100 * total_acc / total_count)