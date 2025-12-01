# -*- coding: utf-8 -*-
"""
新媒体营销与热榜系统 - API接口模块
提供RESTful API接口，连接前后端
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from data_storage import DataStorage
from crawler import ContentCrawler
import threading
import time

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化存储和爬虫
storage = DataStorage()
crawler = ContentCrawler()


@app.route('/api/data', methods=['GET'])
def get_data():
    """
    获取所有数据
    支持查询参数：
    - platform: 平台筛选
    - keyword: 关键词搜索
    """
    try:
        platform = request.args.get('platform')
        keyword = request.args.get('keyword')
        
        if platform:
            data = storage.read_by_platform(platform)
        elif keyword:
            data = storage.search_by_keyword(keyword)
        else:
            data = storage.read_all()
        
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data/<item_id>', methods=['GET'])
def get_data_by_id(item_id):
    """根据ID获取单条数据"""
    try:
        data = storage.read_by_id(item_id)
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': '数据不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data', methods=['POST'])
def create_data():
    """添加新数据"""
    try:
        data = request.get_json()
        success = storage.create(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': '数据添加成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '数据添加失败'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data/<item_id>', methods=['PUT'])
def update_data(item_id):
    """更新数据"""
    try:
        data = request.get_json()
        success = storage.update(item_id, data)
        
        if success:
            return jsonify({
                'success': True,
                'message': '数据更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '数据不存在或更新失败'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data/<item_id>', methods=['DELETE'])
def delete_data(item_id):
    """删除数据"""
    try:
        success = storage.delete(item_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '数据删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '数据不存在或删除失败'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/crawl', methods=['POST'])
def crawl_data():
    """
    触发数据采集
    支持参数：
    - platform: 指定平台（可选）
    """
    try:
        data = request.get_json() or {}
        platform = data.get('platform')
        
        # 在后台线程执行爬取任务
        def crawl_task():
            if platform == '微博':
                results = crawler.crawl_weibo_hot()
            elif platform == '知乎':
                results = crawler.crawl_zhihu_hot()
            elif platform == '抖音':
                results = crawler.crawl_douyin_hot()
            else:
                results = crawler.crawl_all_platforms()
            
            # 保存采集结果
            if results:
                storage.create_batch(results)
        
        thread = threading.Thread(target=crawl_task)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': '数据采集任务已启动'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取数据统计信息"""
    try:
        stats = storage.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """获取所有平台列表"""
    try:
        all_data = storage.read_all()
        platforms = list(set([item.get('platform', '未知') for item in all_data]))
        
        return jsonify({
            'success': True,
            'data': platforms
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'success': True,
        'message': 'API服务正常运行',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })


if __name__ == '__main__':
    print("=" * 50)
    print("新媒体营销与热榜系统 API 服务启动")
    print("API地址: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
