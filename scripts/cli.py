# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - CLI Arayüzü
Kullanım:
  python scripts/cli.py stats
  python scripts/cli.py search "ODTÜ"
  python scripts/cli.py city 06
  python scripts/cli.py compare "06-Ankara/Cankaya/ODTU-Merkez-Kampusu" "34-Istanbul/Sariyer/ITU-Ayazaga-ve-Macka-Taskisla-Kampusleri"
  python scripts/cli.py ask "Deniz kıyısında olan mühendislikler"
  python scripts/cli.py serve --port 8000
  python scripts/cli.py validate
"""

import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kampus_rehberi.cli import main

if __name__ == '__main__':
    main()
