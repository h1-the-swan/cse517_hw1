import sys
stdin = sys.stdin.read()
stdin = stdin.split(u'\n')
logprobs = []
for line in stdin:
    if len(line) > 1:
        try:
            logprobs.append(float(line))
        except ValueError:
            pass
sum = 0
for logprob in logprobs:
    sum += logprob
I = len(logprobs) + 1
perplexity = 2 ** (-(1.0/I) * sum)
print("perplexity:", perplexity)

sum_baseline = 0
for i in range(I-1):
    sum_baseline += -16.0
perplexity_baseline = 2 ** (-(1.0/I) * sum_baseline)
print("perplexity_baseline:", perplexity_baseline)
