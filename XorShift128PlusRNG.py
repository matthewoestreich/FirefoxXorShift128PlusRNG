"""
Simplified implementation of the `XorShift128PlusRNG` class that Firefox uses to generate pseudo-random numbers
in `Math.random`.

Per Mozilla:
 * This generator is not suitable as a cryptographically secure random number
 * generator.

You can check out their implementation here:
https://github.com/mozilla/gecko-dev/blob/f3c8c63a097b61bb1f01e13629b9514e09395947/mfbt/XorShift128PlusRNG.h#L44
"""

"""
The actual XorShift128+ algo they use
```
uint64_t next() {
  uint64_t s1 = mState[0];
  const uint64_t s0 = mState[1];
  mState[0] = s0;
  s1 ^= s1 << 23;
  mState[1] = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26);
  return mState[1] + s0;
}
```
"""

"""
Example usage of this class:
```
xorShift128PlusRNG = FirefoxXorShift128PlusRNG(4412470881888093692, 8243466694241266509)
generated = []
for i in range(10):
  generated.append(xorShift128PlusRNG.nextDouble())
print(generated) # -> [0.7532281207182704, 0.2065075797228122, 0.550024618802937, 0.5216404092901868, 0.23621981172877438, 0.02038275880531304, 0.311432527233898, 0.27575300783729695, 0.9001070256482103, 0.11687926137453397]
```
"""


class FirefoxXorShift128PlusRNG:
    mState = [None, None]

    def __init__(self, initialA, initialB):
        self.mState[0] = initialA
        self.mState[1] = initialB

    def next(self):
        s1 = self.mState[0]
        s0 = self.mState[1]
        self.mState[0] = s0
        s1 ^= s1 << 23
        self.mState[1] = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26)
        return self.mState[1] + s0

    def nextDouble(self):
        kMantissaBits = 52 + 1
        mantissa = self.next() & ((1 << kMantissaBits) - 1)
        return mantissa / (1 << kMantissaBits)
