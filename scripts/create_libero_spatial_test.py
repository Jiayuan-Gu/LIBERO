import os  
import numpy as np  
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates  
from libero.libero.utils.task_generation_utils import register_task_info, generate_bddl_from_task_info  
from libero.libero.utils.bddl_generation_utils import get_xy_region_kwargs_list_from_regions_info  
from libero.libero import get_libero_path  
  
# 场景1：左右角落布局  
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene1(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1, # 新增
        }  
        object_num_info = {  
            "akita_black_bowl": 2,  # 数量改为2
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1, # 新增
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.20, -0.20], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.20, 0.20], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位
        # 炉子放在后方偏左
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.2, -0.2], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方偏右
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.2, 0.2], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))
        
        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            # 新增物品状态
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]  
  
# 场景2：前后布局  
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene2(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, 0.0], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.25, 0.0], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位
        # 炉子放在后方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, 0.25], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在后方左侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, -0.25], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]  
  
# 场景3：对角线布局  
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene3(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):  
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.20, 0.20], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.20, -0.20], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位 (放在另外两个对角)
        # 炉子放在后方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.2, 0.2], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方左侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.2, -0.2], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))
        
        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]  

# 场景4：靠近木柜布局  
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene4(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.05, -0.25], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.10, 0.10], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.15, 0.05], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位 (放在右侧空白区域)
        # 炉子放在后方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.2, 0.25], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.2, 0.25], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]

# 场景5：三角形布局
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene5(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.20, -0.15], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.20, 0.15], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.20], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位
        # 炉子放在后方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, 0.25], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方左侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.25, -0.25], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]

# 场景6：分散布局
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene6(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.05, -0.20], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.15, 0.25], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.10, 0.0], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位
        # 炉子放在后方左侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.2, -0.25], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.2, 0.25], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]

# 场景7：左右对称布局
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene7(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局 (注意：您将黑碗放在右侧 [y=0.25]，盘子放在左侧 [y=-0.25])
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.25], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.25], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位 (放在前后中线)
        # 炉子放在后方
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, 0.0], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.25, 0.0], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]

# 场景8：前后遮挡布局
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene8(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.15, 0.10], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.20, -0.10], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.05, 0.15], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位
        # 炉子放在后方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, 0.25], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方左侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.25, -0.25], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]

# 场景9：横向线性布局
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene9(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.25, 0.05], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.05, 0.05], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, 0.05], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位 (放在后方)
        # 炉子放在后方右侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.2, 0.25], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在后方左侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.2, -0.25], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]
    
# 场景10：远近布局
@register_mu(scene_type="kitchen")  
class KitchenSpatialTestScene10(InitialSceneTemplates):  
    def __init__(self):  
        fixture_num_info = {  
            "kitchen_table": 1,  
            "wooden_cabinet": 1,
            "flat_stove": 1,
        }  
        object_num_info = {  
            "akita_black_bowl": 2,
            "plate": 1,  
            "glazed_rim_porcelain_ramekin": 1,
            "cookies": 1,
        }  
        super().__init__(  
            workspace_name="kitchen_table",  
            fixture_num_info=fixture_num_info,  
            object_num_info=object_num_info,  
        )  
  
    def define_regions(self):
        # 原有物品布局 (注意：盘子已在 [0.25, 0.25])
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.10, -0.20], region_name="akita_black_bowl_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, 0.25], region_name="plate_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.10, 0.0], region_name="ramekin_init_region", target_name=self.workspace_name, region_half_len=0.025))  
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, -0.30], region_name="wooden_cabinet_init_region", target_name=self.workspace_name, region_half_len=0.01, yaw_rotation=(np.pi, np.pi)))
        
        # 为新增物品寻找合理空位
        # 炉子放在后方左侧 (因为右侧已被盘子占据)
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.25, -0.25], region_name="flat_stove_init_region", target_name=self.workspace_name, region_half_len=0.05))
        # 饼干盒放在前方左侧
        self.regions.update(self.get_region_dict(region_centroid_xy=[-0.25, -0.25], region_name="cookies_init_region", target_name=self.workspace_name, region_half_len=0.03))
        # 定义炉子上的烹饪区域
        self.regions.update(self.get_region_dict(region_centroid_xy=[0.0, 0.0], region_name="cook_region", target_name="flat_stove_1", region_half_len=0.025))

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(self.regions)  
  
    @property  
    def init_states(self):  
        return [  
            ("On", "akita_black_bowl_1", "kitchen_table_akita_black_bowl_init_region"),  
            ("On", "plate_1", "kitchen_table_plate_init_region"),  
            ("On", "glazed_rim_porcelain_ramekin_1", "kitchen_table_ramekin_init_region"),  
            ("On", "wooden_cabinet_1", "kitchen_table_wooden_cabinet_init_region"),
            ("On", "flat_stove_1", "kitchen_table_flat_stove_init_region"),
            ("On", "cookies_1", "kitchen_table_cookies_init_region"),
            ("On", "akita_black_bowl_2", "flat_stove_1_cook_region"),
        ]


def create_spatial_test_tasks():  
    """创建10个新的空间任务"""  
    tasks = [  
        ("pick_up_the_black_bowl_from_left_corner_and_place_it_on_the_right_plate", "kitchen_spatial_test_scene1"),  
        ("pick_up_the_black_bowl_behind_the_ramekin_and_place_it_on_the_front_plate", "kitchen_spatial_test_scene2"),  
        ("pick_up_the_black_bowl_from_far_left_and_place_it_on_the_center_plate", "kitchen_spatial_test_scene3"),  
        ("pick_up_the_black_bowl_near_the_cabinet_edge_and_place_it_on_the_plate", "kitchen_spatial_test_scene4"),  
        ("pick_up_the_black_bowl_from_table_corner_and_place_it_on_the_opposite_plate", "kitchen_spatial_test_scene5"),  
        ("pick_up_the_black_bowl_beside_the_wooden_cabinet_and_place_it_on_the_plate", "kitchen_spatial_test_scene6"),  
        ("pick_up_the_black_bowl_from_right_side_and_place_it_on_the_left_plate", "kitchen_spatial_test_scene7"),  
        ("pick_up_the_black_bowl_in_front_of_ramekin_and_place_it_on_the_back_plate", "kitchen_spatial_test_scene8"),  
        ("pick_up_the_black_bowl_from_near_edge_and_place_it_on_the_central_plate", "kitchen_spatial_test_scene9"),  
        ("pick_up_the_black_bowl_adjacent_to_cabinet_and_place_it_on_the_distant_plate", "kitchen_spatial_test_scene10"),  
    ]  
      
    for language, scene_name in tasks:  
        register_task_info(  
            language,  
            scene_name=scene_name,  
            # 目标物体仍然是第一个黑碗和盘子
            objects_of_interest=["akita_black_bowl_1", "plate_1"],  
            goal_states=[("On", "akita_black_bowl_1", "plate_1")]  
        )  
  
def main():  
    # 注册新任务  
    create_spatial_test_tasks()  
      
    # 获取正确的BDDL文件保存路径  
    bddl_base_path = get_libero_path("bddl_files")  
    target_folder = os.path.join(bddl_base_path, "libero_spatial_test")  
      
    # 生成BDDL文件  
    bddl_files, failures = generate_bddl_from_task_info(folder=target_folder)  
      
    print(f"成功生成 {len(bddl_files)} 个BDDL文件")  
    print(f"保存路径: {target_folder}")  
    if failures:  
        print(f"失败的任务: {failures}")  
      
    return bddl_files, failures  
  
if __name__ == "__main__":  
    main()
