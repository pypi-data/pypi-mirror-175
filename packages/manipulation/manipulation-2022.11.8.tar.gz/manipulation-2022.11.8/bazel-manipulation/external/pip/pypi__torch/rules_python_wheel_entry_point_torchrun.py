#!/usr/bin/env python3
import sys
from torch.distributed.run import main
if __name__ == "__main__":
    rc = main()
    sys.exit(main())
