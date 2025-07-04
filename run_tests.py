#!/usr/bin/env python3
"""
Script para executar todos os testes do módulo ClickUp
"""

import unittest
import sys
import os

# Adiciona o diretório src ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_all_tests():
    """Executa todos os testes e retorna o resultado"""
    
    # Descobre e carrega todos os testes
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_specific_test(test_file):
    """Executa um teste específico"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.{test_file}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Executa teste específico
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Executa todos os testes
        success = run_all_tests()
    
    # Retorna código de saída apropriado
    sys.exit(0 if success else 1) 