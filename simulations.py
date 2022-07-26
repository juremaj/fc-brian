from brian2 import *
import matplotlib.pyplot as plt
import numpy as np

start_scope()

sig = 0.1

eqs = '''
dv/dt = (I-v)/tau + sig*xi*tau**-0.5: 1
I : 1
tau : second
'''

N = 200
G = NeuronGroup(N, eqs, threshold='v>1', reset='v = 0', method='euler')
G.I = 1.1
G.tau = 100*ms

S = Synapses(G, G)
S.connect(condition='i!=j', p=0.01)
#S.w = ... to define strength of weight

spikemon = SpikeMonitor(G)

run_for = 100
run(run_for*second)

plt.figure(figsize=(20, 4))
plt.scatter(spikemon.t[spikemon.i<100]/ms, spikemon.i[spikemon.i<100], s=1, c='k') # t is spike time, i is neuron id
xlabel('Time (ms)')
ylabel('Neuron index')
savefig('spiking_data.png')

# bin spikes at 30Hz
plt.figure(figsize=(20, 4))
imaging_rate = 30 
n_neurons = 100
all_hist = np.zeros((n_neurons, run_for*imaging_rate))
for n in range(n_neurons):
    all_hist[n,:] = np.histogram(spikemon.t[spikemon.i==n], bins=np.arange(0,run_for+0.00001,1/imaging_rate))[0]
    #all_hist.append(n_hist[0])
plt.imshow(all_hist)
savefig(f'binned_30.png')

figure()
scatter(S.i, S.j, s=1, c='k')
savefig('ground_truth.png')

print('test')