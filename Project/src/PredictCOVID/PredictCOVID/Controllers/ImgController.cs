using PredictCOVID.Service;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace PredictCOVID.Controllers
{
    public class ImgController : Controller
    {
        // GET: Img
        public ActionResult showImg(String id)
        {
            UserService service = new UserService();
            String photo = service.findByName(id).PHOTO;
            var dir = AppDomain.CurrentDomain.BaseDirectory;
            dir = dir.Replace("\\src\\PredictCOVID\\PredictCOVID\\", "");
            dir += "\\image\\TrainImage\\" + id;
            var path = Path.Combine(dir, photo);
            return base.File(path, "image");
        }
    }
}