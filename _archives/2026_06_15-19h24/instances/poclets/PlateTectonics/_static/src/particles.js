// Systèmes de particules
function buildParticles() {
  const dot = mkDot();
  
  function createPS(nm, cap, ex, ey, ez, mBx, mBy, mBz, MBx, MBy, MBz, c1, c2, d1, d2, mS, MS, mL, ML, rate) {
    const p = new BABYLON.ParticleSystem(nm, cap, scene);
    p.particleTexture = new BABYLON.Texture(dot, scene);
    p.emitter = new BABYLON.Vector3(ex, ey, ez);
    p.minEmitBox = new BABYLON.Vector3(mBx, mBy, mBz);
    p.maxEmitBox = new BABYLON.Vector3(MBx, MBy, MBz);
    p.color1 = new BABYLON.Color4(...c1);
    p.color2 = new BABYLON.Color4(...c2);
    p.colorDead = new BABYLON.Color4(0, 0, 0, 0);
    p.minSize = mS;
    p.maxSize = MS;
    p.minLifeTime = mL;
    p.maxLifeTime = ML;
    p.emitRate = rate;
    p.direction1 = new BABYLON.Vector3(...d1);
    p.direction2 = new BABYLON.Vector3(...d2);
    p.minEmitPower = .15;
    p.maxEmitPower = .65;
    p.gravity = new BABYLON.Vector3(0, -.04, 0);
    return p;
  }
  
  psConv = createPS('psC', 180, 0, -2, 0, -6.5, -.7, -2.2, 6.5, .7, 2.2, [1, .52, .10, .70], [.80, .20, .04, .45], [-0.3, .9, .2], [.3, .9, -.2], .10, .35, 3, 7, 28);
  psRidge = createPS('psR', 100, 0, -.1, 0, -.4, 0, -2.2, .4, 0, 2.2, [1, .65, .12, .92], [1, .30, .04, .72], [-.04, 1, .04], [.04, 1, -.04], .07, .16, 1, 2.5, 18);
  psVol = createPS('psV', 60, 3.8, 2.3, .3, -.08, 0, -.08, .08, 0, .08, [1, .40, .05, .92], [.85, .18, .02, .65], [-.5, 1, -.5], [.5, 1, .5], .06, .14, 1.4, 2.8, 10);
  psQuake = createPS('psQ', 80, 0, .80, 0, -.1, 0, -2, .1, 0, 2, [1, .80, .20, .92], [1, .40, .10, .70], [-.7, 1, -.7], [.7, 1, .7], .08, .20, .6, 1.6, 0);
  psQuake.targetStopDuration = .7;
   
  psConv.start();
  psRidge.start();
  psVol.start();
}