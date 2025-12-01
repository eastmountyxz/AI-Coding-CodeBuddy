# -*- coding: utf-8 -*-
"""
新媒体营销与热榜系统 - 数据存储模块
使用JSON进行结构化数据存储，支持增删查改操作
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class DataStorage:
    """JSON数据存储管理类"""
    
    def __init__(self, filename: str = "data.json"):
        self.filename = filename
        self.data = []
        self.load_data()
    
    def load_data(self):
        """从JSON文件加载数据"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"成功加载 {len(self.data)} 条数据")
            else:
                self.data = []
                print("数据文件不存在，创建新文件")
        except json.JSONDecodeError:
            print("JSON文件格式错误，初始化为空数据")
            self.data = []
        except Exception as e:
            print(f"加载数据失败: {e}")
            self.data = []
    
    def save_data(self):
        """保存数据到JSON文件"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"成功保存 {len(self.data)} 条数据")
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def create(self, item: Dict) -> bool:
        """
        增：添加新数据
        :param item: 要添加的数据字典
        :return: 是否成功
        """
        try:
            # 添加唯一ID
            if 'id' not in item:
                item['id'] = self._generate_id()
            
            # 添加创建时间
            if 'created_at' not in item:
                item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            self.data.append(item)
            self.save_data()
            print(f"成功添加数据，ID: {item['id']}")
            return True
        except Exception as e:
            print(f"添加数据失败: {e}")
            return False
    
    def create_batch(self, items: List[Dict]) -> int:
        """
        批量添加数据
        :param items: 数据列表
        :return: 成功添加的数量
        """
        success_count = 0
        for item in items:
            try:
                if 'id' not in item:
                    item['id'] = self._generate_id()
                if 'created_at' not in item:
                    item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.data.append(item)
                success_count += 1
            except Exception as e:
                print(f"添加单条数据失败: {e}")
        
        if success_count > 0:
            self.save_data()
        print(f"批量添加完成，成功 {success_count}/{len(items)} 条")
        return success_count
    
    def read_all(self) -> List[Dict]:
        """
        查：读取所有数据
        :return: 数据列表
        """
        return self.data
    
    def read_by_id(self, item_id: str) -> Optional[Dict]:
        """
        查：根据ID读取单条数据
        :param item_id: 数据ID
        :return: 数据字典或None
        """
        for item in self.data:
            if item.get('id') == item_id:
                return item
        return None
    
    def read_by_platform(self, platform: str) -> List[Dict]:
        """
        查：根据平台筛选数据
        :param platform: 平台名称
        :return: 符合条件的数据列表
        """
        return [item for item in self.data if item.get('platform') == platform]
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """
        查：根据关键词搜索数据
        :param keyword: 搜索关键词
        :return: 包含关键词的数据列表
        """
        results = []
        keyword_lower = keyword.lower()
        
        for item in self.data:
            # 在标题、摘要等字段中搜索
            title = item.get('title', '').lower()
            excerpt = item.get('excerpt', '').lower()
            category = item.get('category', '').lower()
            
            if keyword_lower in title or keyword_lower in excerpt or keyword_lower in category:
                results.append(item)
        
        return results
    
    def update(self, item_id: str, updated_data: Dict) -> bool:
        """
        改：更新数据
        :param item_id: 数据ID
        :param updated_data: 更新的数据字典
        :return: 是否成功
        """
        for i, item in enumerate(self.data):
            if item.get('id') == item_id:
                # 保留原有ID和创建时间
                updated_data['id'] = item_id
                if 'created_at' in item:
                    updated_data['created_at'] = item['created_at']
                
                # 添加更新时间
                updated_data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                self.data[i] = updated_data
                self.save_data()
                print(f"成功更新数据，ID: {item_id}")
                return True
        
        print(f"未找到ID为 {item_id} 的数据")
        return False
    
    def delete(self, item_id: str) -> bool:
        """
        删：删除数据
        :param item_id: 数据ID
        :return: 是否成功
        """
        for i, item in enumerate(self.data):
            if item.get('id') == item_id:
                del self.data[i]
                self.save_data()
                print(f"成功删除数据，ID: {item_id}")
                return True
        
        print(f"未找到ID为 {item_id} 的数据")
        return False
    
    def delete_by_platform(self, platform: str) -> int:
        """
        删除指定平台的所有数据
        :param platform: 平台名称
        :return: 删除的数量
        """
        original_count = len(self.data)
        self.data = [item for item in self.data if item.get('platform') != platform]
        deleted_count = original_count - len(self.data)
        
        if deleted_count > 0:
            self.save_data()
        print(f"删除了 {deleted_count} 条 {platform} 平台的数据")
        return deleted_count
    
    def clear_all(self) -> bool:
        """
        清空所有数据
        :return: 是否成功
        """
        self.data = []
        self.save_data()
        print("已清空所有数据")
        return True
    
    def get_statistics(self) -> Dict:
        """
        获取数据统计信息
        :return: 统计信息字典
        """
        stats = {
            'total_count': len(self.data),
            'platform_count': {},
            'category_count': {},
            'latest_update': None
        }
        
        # 统计各平台数量
        for item in self.data:
            platform = item.get('platform', '未知')
            stats['platform_count'][platform] = stats['platform_count'].get(platform, 0) + 1
            
            category = item.get('category', '未分类')
            stats['category_count'][category] = stats['category_count'].get(category, 0) + 1
        
        # 获取最新更新时间
        if self.data:
            timestamps = [item.get('timestamp', item.get('created_at', '')) for item in self.data]
            stats['latest_update'] = max(timestamps) if timestamps else None
        
        return stats
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return str(uuid.uuid4())


# 使用示例
if __name__ == "__main__":
    # 初始化存储
    storage = DataStorage()
    
    # 示例：添加数据
    sample_data = {
        'platform': '微博',
        'title': '测试热搜',
        'link': 'https://weibo.com/test',
        'rank': 1,
        'category': '热搜'
    }
    storage.create(sample_data)
    
    # 查询所有数据
    all_data = storage.read_all()
    print(f"总共 {len(all_data)} 条数据")
    
    # 获取统计信息
    stats = storage.get_statistics()
    print("统计信息:", json.dumps(stats, ensure_ascii=False, indent=2))
