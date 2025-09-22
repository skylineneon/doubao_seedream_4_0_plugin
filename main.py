from dify_plugin import Plugin, DifyPluginEnv

# 配置插件环境，设置超长超时时间以适应图像生成的时间需求
# 增加到 1200 秒（20分钟）以彻底解决 BrokenPipeError
plugin = Plugin(DifyPluginEnv(MAX_REQUEST_TIMEOUT=600))

if __name__ == "__main__":
    plugin.run()
