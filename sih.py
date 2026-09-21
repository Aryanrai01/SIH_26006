cv2.putText(canvas, f"POV: {ego_name}", (8, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1)
                
                payload_str = self.payload_status[ego_id]
                dist_label = f"RANGE: {closest_dist:.1f}m" if target_seen else "CLEAR: >45m"
                col_hud = (0, 230, 255) if (not target_seen or closest_dist > 6.0) else (0, 0, 255)
                speed_kmh = self.speeds[ego_id] * 3.6
                
                cv2.putText(canvas, f"{dist_label} | {speed_kmh:.1f} km/h", (8, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.38, col_hud, 1)
                cv2.putText(canvas, f"PAYLOAD: {payload_str}", (8, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (180, 255, 180), 1)

                msg = self.bridge.cv2_to_imgmsg(canvas, encoding="bgr8")
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = f"dumper_{ego_id}_cam"
                self.pub_cams[ego_id].publish(msg)

                row, col = grid_positions[ego_id]
                y_start = 45 + row * tile_h
                y_end = y_start + tile_h
                x_start = col * tile_w
                x_end = x_start + tile_w
                dashboard[y_start:y_end, x_start:x_end] = canvas

            self.pub_cockpit.publish(self.bridge.cv2_to_imgmsg(dashboard, encoding="bgr8"))

def main(args=None):
    rclpy.init(args=args)
    node = BailadilaProductionEngine()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if name == 'main':
    main()
EOF
