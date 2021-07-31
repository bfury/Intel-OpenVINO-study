1、学习OpenVINO多路视频处理原理。

2、使用OpenVINO进行多路视频处理。

进行单段视频的人员检测和跟踪。

`python3 multi_camera_multi_person_tracking.py --m_detector models/person-detection-retail-0013.xml --m_reid models/person-reidentification-retail-0300.xml --config config.py -i Videos/video2.avi`

执行如下命令，用no_show和output选项将人员检测和跟踪的结果视频保存到输出文件。

` python3 multi_camera_multi_person_tracking.py --m_detector models/person-detection-retail-0013.xml --m_reid models/person-reidentification-retail-0300.xml --config config.py -i Videos/video2.avi --no_show --output out.avi`

执行如下命令，进行多段视频的人员检测和跟踪。

`python3 multi_camera_multi_person_tracking.py --m_detector models/person-detection-retail-0013.xml --m_reid models/person-reidentification-retail-0300.xml --config config.py -i Videos/video1.avi Videos/video2.avi Videos/video3.avi`



