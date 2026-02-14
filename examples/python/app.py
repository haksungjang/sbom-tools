#!/usr/bin/env python3
"""
SBOM Example Application - Flask API

간단한 Flask 기반 REST API 애플리케이션입니다.
SBOM 생성 테스트를 위한 예제입니다.
"""

from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
def home():
    """메인 엔드포인트"""
    return jsonify({
        'message': 'SBOM Example Application is running!',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health')
def health():
    """헬스 체크 엔드포인트"""
    return jsonify({'status': 'OK'})


@app.route('/data', methods=['GET'])
def get_data():
    """샘플 데이터 반환"""
    # Pandas와 NumPy 사용 예시
    data = pd.DataFrame({
        'id': np.arange(1, 11),
        'value': np.random.rand(10),
        'label': [f'Item {i}' for i in range(1, 11)]
    })
    
    return jsonify({
        'data': data.to_dict(orient='records'),
        'count': len(data)
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    """간단한 데이터 분석"""
    data = request.get_json()
    
    if not data or 'numbers' not in data:
        return jsonify({'error': 'numbers field is required'}), 400
    
    numbers = data['numbers']
    
    result = {
        'mean': float(np.mean(numbers)),
        'median': float(np.median(numbers)),
        'std': float(np.std(numbers)),
        'min': float(np.min(numbers)),
        'max': float(np.max(numbers))
    }
    
    return jsonify(result)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
