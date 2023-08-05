# To Study the PN Sequence Generator

# Solve for
# 1. g(x) = x^3 + x + 1
# 2. g(x) = x^4 + x + 1
from matplotlib import pyplot as plt

'''
1. Calculate:
    - code_len/iterations = 2^n - 1
    - state = n 1's
    - output = []

2. iterate code_len times:
    - append state LSB (last value) to output
    - calculate new state based on equation 
    - print output

3. plot output using plt.stem method
'''

def pol3():
    # g(x) = x^3 + x + 1
    iterations = 2**3 - 1 # number of iterations
    state = [1,1,1] # initial state
    output = []

    print(f'0:\t{state}')
    
    for i in range(iterations):
        # start with 
        output.append(state[2])
        state = [state[1]^state[2], state[0], state[1]]
        print(f'{i+1}:\t{state}')
    
    print(output)
    plt.stem(output)
    plt.title('M-Sequence generated for g(x) = x^3 + x + 1')
    plt.show()

def pol4():
    # g(x) = x^4 + x + 1
    iterations = 2**4 - 1
    state = [1,1,1,1]
    output = []

    print(f'0:\t{state}')
    
    for i in range(iterations):
        output.append(state[3])
        state = [state[3]^state[2], state[0], state[1], state[2]]
        print(f'{i+1}:\t{state}')
    
    print(output)
    plt.stem(output)
    plt.title('M-Sequence generated for g(x) = x^4 + x + 1')
    plt.show()


class PNG:
    '''
    only works for x^n + x + 1 generator polynomial
    '''
    def __init__(self, polynomial_taps: list) -> None:
        assert isinstance(polynomial_taps, list)

        # set tap values
        self.taps_index = polynomial_taps
        try:
            self.taps_index.remove(0)
        except ValueError:
            pass

        # get output length and iterations
        self.output_len = max(polynomial_taps)
        self.iterations = 2**self.output_len - 1

        # set initial state to 1's
        self.state = [1 for _ in range(self.output_len)]


    def generate(self):
        output = []
        print(f'0:\t{self.state}')

        for i in range(self.iterations):
            output.append(self.state[self.output_len-1])
            new_bit = self.state[self.output_len-1] ^ self.state[self.output_len-2]
            self.state.pop()
            self.state.insert(0, new_bit)
            print(f'{i+1}:\t{self.state}')
        
        print(output)
        plt.stem(output)
        plt.title(f'M-Sequence generated for g(x) = x^{self.output_len} + x + 1')
        plt.show()
            

if __name__ == '__main__':
    PNG(
        polynomial_taps=[3, 1, 0],
    ).generate()

    PNG(
        polynomial_taps=[4, 1, 0],
    ).generate()